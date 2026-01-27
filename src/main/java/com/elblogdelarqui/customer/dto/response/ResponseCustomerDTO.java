package com.elblogdelarqui.customer.dto.response;

import com.elblogdelarqui.customer.entity.Customer;
import lombok.Getter;

import java.io.Serializable;
import java.util.Date;

@Getter
public class ResponseCustomerDTO implements Serializable {
    private Long id;
    private String firstName;
    private String lastName;
    private Date birthDate;
    private String address;
    private String city;
    private String country;
    private String phone;
    private Integer age;

    public ResponseCustomerDTO(Customer customer) {
        this.id = customer.getId();
        this.firstName = customer.getFirstName();
        this.lastName = customer.getLastName();
        this.birthDate = customer.getBirthDate();
        this.address = customer.getAddress();
        this.city = customer.getCity();
        this.country = customer.getCountry();
        this.phone = customer.getPhone();
        this.age = customer.getAge();
    }
}
