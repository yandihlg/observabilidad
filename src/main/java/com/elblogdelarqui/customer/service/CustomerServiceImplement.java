package com.elblogdelarqui.customer.service;

import com.elblogdelarqui.customer.dto.request.RequestCustomerDTO;
import com.elblogdelarqui.customer.dto.response.ResponseCustomerDTO;
import com.elblogdelarqui.customer.entity.Customer;
import com.elblogdelarqui.customer.publisher.RabbitMQProducer;
import com.elblogdelarqui.customer.repository.CustomerRepository;
import com.elblogdelarqui.customer.util.CustomerMapper;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.cache.annotation.Cacheable;
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

import java.io.IOException;
import java.util.List;

@Service
@Primary
public class CustomerServiceImplement implements CustomerService {

    private final CustomerRepository customerRepository;
    private final CustomerMapper customerMapper; //
    private final RabbitMQProducer rabbitMQProducer;
    private final EmailService emailService;
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    public CustomerServiceImplement(CustomerRepository customerRepository,
                                    CustomerMapper customerMapper,
                                    RabbitMQProducer rabbitMQProducer,
                                    EmailService emailService) {
        this.customerRepository = customerRepository;
        this.customerMapper = customerMapper;
        this.rabbitMQProducer = rabbitMQProducer;
        this.emailService = emailService;
    }

    @Override
    @Cacheable(value = "myCache", key = "'customer_' + #id")
    public ResponseCustomerDTO findById(Long id) {
        Span span = tracer.spanBuilder("customer.service.findById")
                .setAttribute("customer.id", id)
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            Customer customer = returnCustomer(id);
            ResponseCustomerDTO response = customerMapper.toCustomerDTO(customer);
            span.addEvent("customer.found", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.firstName", customer.getFirstName())
                    .put("customer.phone", customer.getPhone())
                    .build());
            return response;
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }

    @Override
    public List<ResponseCustomerDTO> findAll() {
        List<Customer> customerList = (customerRepository.findAll());
        return customerMapper.toCustomerDTO(customerList);
    }

    @Override
    public ResponseCustomerDTO register(RequestCustomerDTO customerDTO) throws IOException {
        Span span = tracer.spanBuilder("customer.service.register")
                .setAttribute("customer.firstName", customerDTO.getFirstName())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            Customer customer = customerMapper.toCustomer(customerDTO);
            customer = customerRepository.save(customer);
            span.addEvent("customer.saved", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.id", customer.getId())
                    .build());

            ObjectMapper objectMapper = new ObjectMapper();
            String event = objectMapper.writeValueAsString(customer);

            rabbitMQProducer.sendMessage(event);
            span.addEvent("message.sent.rabbitmq");
            
            emailService.sendEmail("Create Customer", event);
            span.addEvent("email.sent");

            return customerMapper.toCustomerDTO(customer);
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }


    @Override
    public ResponseCustomerDTO update(Long id, RequestCustomerDTO customerDTO) {
        Customer customer = returnCustomer(id);
        customerMapper.updateCustomer(customer, customerDTO);
        customer = customerRepository.save(customer);
        return customerMapper.toCustomerDTO(customer);

    }

    @Override
    public String delete(Long id) {
        customerRepository.deleteById(id);
        return "Customer id: " + id + " deleted";
    }

    private Customer returnCustomer(Long id) {
        return customerRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer wasn't fount on database"));
    }
}
