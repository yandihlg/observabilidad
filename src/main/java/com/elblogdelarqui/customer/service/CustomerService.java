package com.elblogdelarqui.customer.service;

import com.elblogdelarqui.customer.dto.request.RequestCustomerDTO;
import com.elblogdelarqui.customer.dto.response.ResponseCustomerDTO;

import java.io.IOException;
import java.util.List;

public interface CustomerService {
    ResponseCustomerDTO findById(Long id);
    List<ResponseCustomerDTO> findAll();
    ResponseCustomerDTO register (RequestCustomerDTO customerDTO) throws IOException;
    ResponseCustomerDTO update(Long id, RequestCustomerDTO customerDTO);
    String delete(Long id);
}