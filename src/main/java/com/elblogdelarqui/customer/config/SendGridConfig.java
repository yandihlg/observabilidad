package com.elblogdelarqui.customer.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SendGridConfig {
    @Value("${sendgrid.api.key}")
    private String sendGridApiKey;

    @Value("${sendgrid.api.from}")
    private String sendGridApiFrom;

    @Value("${sendgrid.api.to}")
    private String sendGridApiTo;
}
