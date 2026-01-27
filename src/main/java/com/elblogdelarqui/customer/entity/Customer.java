package com.elblogdelarqui.customer.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;

@Entity
@Table(name = "Customers")
@NoArgsConstructor
@Getter
@Setter
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false, unique = true)
    @Setter(AccessLevel.NONE)
    private Long id;

    @Column(name = "firstName", nullable = false)
    private String firstName;

    @Column(name = "lastName", nullable = false)
    private String lastName;

    @Column(name = "birthDate", nullable = false)
    private Date birthDate;

    @Column(name = "address", nullable = false)
    private String address;

    @Column(name = "city", nullable = false)
    private String city;

    @Column(name = "country", nullable = false)
    private String country;

    @Column(name = "phone", nullable = false)
    private String phone;

    @Column(name = "age", nullable = false)
    private Integer age;

    @Builder
     public Customer(String firstName,
                     String lastName,
                     Date birthDate,
                     String address,
                     String city,
                     String country,
                     String phone,
                     Integer age) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.birthDate = birthDate;
        this.address = address;
        this.city = city;
        this.country = country;
        this.phone = phone;
        this.age = age;
    }
}
