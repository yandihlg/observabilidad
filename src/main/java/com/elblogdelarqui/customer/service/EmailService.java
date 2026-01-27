package com.elblogdelarqui.customer.service;

import com.sendgrid.helpers.mail.Mail;
import org.springframework.stereotype.Service;
import java.io.IOException;
import org.springframework.beans.factory.annotation.Value;
import com.sendgrid.helpers.mail.objects.*;
import com.sendgrid.Method;
import com.sendgrid.Request;
import com.sendgrid.Response;
import com.sendgrid.SendGrid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class EmailService {
    @Value("${sendgrid.api.key}")
    private String sendGridApiKey;

    @Value("${sendgrid.api.from}")
    private String sendGridApiFrom;

    @Value("${sendgrid.api.to}")
    private String sendGridApiTo;

    private static final Logger logger = LoggerFactory.getLogger(EmailService.class);

    public void sendEmail(String subject, String content) throws IOException {
        logger.info(String.valueOf("Payload: " + content));
        Email from = new Email(sendGridApiFrom);
        Email toEmail = new Email(sendGridApiTo);
        Content emailContent = new Content("text/plain", content);
        Mail mail = new Mail(from, subject, toEmail, emailContent);
        SendGrid sg = new SendGrid(sendGridApiKey);
        Request request = new Request();
        request.setMethod(Method.POST);
        request.setEndpoint("mail/send");
        request.setBody(mail.build());
        Response response = sg.api(request);
        logger.info(String.valueOf("StatusCode: " + response.getStatusCode()));
    }
}
