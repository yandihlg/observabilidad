package com.elblogdelarqui.customer.dto.request;

import lombok.Getter;

import java.util.Date;

@Getter

public class RequestCustomerDTO {

    private String firstName;
    private String lastName;
    private Date birthDate;
    private String address;
    private String city;
    private String country;
    private String phone;
    private Integer age;
}
