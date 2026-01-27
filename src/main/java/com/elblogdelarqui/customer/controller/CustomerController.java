package com.elblogdelarqui.customer.controller;

import com.elblogdelarqui.customer.dto.request.RequestCustomerDTO;
import com.elblogdelarqui.customer.dto.response.ResponseCustomerDTO;
import com.elblogdelarqui.customer.service.CustomerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

import java.io.IOException;
import java.net.URI;
import java.util.List;

@RestController
@RequestMapping(value = "/api/customer")
public class CustomerController {
    private final CustomerService customerService;
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<ResponseCustomerDTO> findById(@PathVariable(name = "id") Long id) {
        Span span = tracer.spanBuilder("http.get.findById")
                .setAttribute("http.method", "GET")
                .setAttribute("http.route", "/api/customer/{id}")
                .setAttribute("customer.id", id)
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            ResponseCustomerDTO response = customerService.findById(id);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.ok().body(response);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    @GetMapping
    public ResponseEntity<List<ResponseCustomerDTO>> findAll() throws IOException {
        Span span = tracer.spanBuilder("http.get.findAll")
                .setAttribute("http.method", "GET")
                .setAttribute("http.route", "/api/customer")
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            List<ResponseCustomerDTO> customers = customerService.findAll();
            span.addEvent("customers.retrieved", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.count", customers.size())
                    .build());
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.ok().body(customers);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    @PostMapping
    public ResponseEntity<ResponseCustomerDTO> register (@RequestBody RequestCustomerDTO customerDTO,
                                                         UriComponentsBuilder uriBuilder) throws IOException {
        Span span = tracer.spanBuilder("http.post.register")
                .setAttribute("http.method", "POST")
                .setAttribute("http.route", "/api/customer")
            .setAttribute("customer.firstName", customerDTO.getFirstName())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            ResponseCustomerDTO responseCustomerDTO = customerService.register(customerDTO);
            span.addEvent("customer.registered", 
                io.opentelemetry.api.common.Attributes.builder()
                    .put("customer.id", responseCustomerDTO.getId())
                    .build());
            URI uri = uriBuilder.path("/api/customer/{id}").buildAndExpand(responseCustomerDTO.getId()).toUri();
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.created(uri).body(responseCustomerDTO);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    @PutMapping(value = "/{id}")
    public ResponseEntity<ResponseCustomerDTO> update(@RequestBody RequestCustomerDTO customerDTO,
                                                      @PathVariable(name = "id") Long id) {
        Span span = tracer.spanBuilder("http.put.update")
                .setAttribute("http.method", "PUT")
                .setAttribute("http.route", "/api/customer/{id}")
                .setAttribute("customer.id", id)
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            ResponseCustomerDTO response = customerService.update(id, customerDTO);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.ok().body(response);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    @DeleteMapping(value = "/{id}")
    public ResponseEntity<String> delete(@PathVariable (value = "id") Long id) {
        Span span = tracer.spanBuilder("http.delete.delete")
                .setAttribute("http.method", "DELETE")
                .setAttribute("http.route", "/api/customer/{id}")
                .setAttribute("customer.id", id)
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            String response = customerService.delete(id);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.OK);
            return ResponseEntity.ok().body(response);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
