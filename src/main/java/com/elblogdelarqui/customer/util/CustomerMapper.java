package com.elblogdelarqui.customer.util;

import com.elblogdelarqui.customer.dto.request.RequestCustomerDTO;
import com.elblogdelarqui.customer.dto.response.ResponseCustomerDTO;
import com.elblogdelarqui.customer.entity.Customer;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

@Component

public class CustomerMapper {
    public Customer toCustomer(RequestCustomerDTO customerDTO) {
        return Customer.builder()
                .firstName(customerDTO.getFirstName())
                .lastName(customerDTO.getLastName())
                .birthDate(customerDTO.getBirthDate())
                .address(customerDTO.getAddress())
                .city(customerDTO.getCity())
                .country(customerDTO.getCountry())
                .phone(customerDTO.getPhone())
                .age(customerDTO.getAge())
                .build();
    }
    public ResponseCustomerDTO toCustomerDTO(Customer customer) {
        return new ResponseCustomerDTO(customer);
    }

    public List<ResponseCustomerDTO> toCustomerDTO(List<Customer> customerList) {
        return customerList.stream().map(ResponseCustomerDTO::new).collect(Collectors.toList());
    }

    public void updateCustomer(Customer customer, RequestCustomerDTO customerDTO) {
        customer.setFirstName(customerDTO.getFirstName());
        customer.setLastName(customerDTO.getLastName());
        customer.setBirthDate(customerDTO.getBirthDate());
        customer.setAddress(customerDTO.getAddress());
        customer.setCity(customerDTO.getCity());
        customer.setCountry(customerDTO.getCountry());
        customer.setPhone(customerDTO.getPhone());
        customer.setAge(customerDTO.getAge());
    }
}