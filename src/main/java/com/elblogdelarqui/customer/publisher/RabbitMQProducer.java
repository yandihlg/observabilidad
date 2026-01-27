package com.elblogdelarqui.customer.publisher;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Scope;

@Service
public class RabbitMQProducer {
    @Value("${rabbitmq.exchange.name}")
    private String exchange;

    @Value("${rabbitmq.routing.key}")
    private String routingKey;

    private static final Logger LOGGER = LoggerFactory.getLogger(RabbitMQProducer.class);
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("com.elblogdelarqui.customer");

    private RabbitTemplate rabbitTemplate;

    public RabbitMQProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendMessage(String message){
        Span span = tracer.spanBuilder("rabbitmq.publish")
                .setAttribute("messaging.system", "rabbitmq")
                .setAttribute("messaging.destination", exchange)
                .setAttribute("messaging.rabbitmq.routing_key", routingKey)
                .setAttribute("messaging.message_payload_size_bytes", message.length())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            LOGGER.info(String.format("Message sent -> %s", message));
            rabbitTemplate.convertAndSend(exchange, routingKey, message);
            span.addEvent("message.published");
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
