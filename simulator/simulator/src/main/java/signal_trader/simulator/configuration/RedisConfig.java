package signal_trader.simulator.configuration;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.listener.PatternTopic;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import signal_trader.simulator.service.SignalSubscriber;

@Configuration
public class RedisConfig {
    @Bean
    public RedisMessageListenerContainer redisContainer(RedisConnectionFactory connectionFactory, SignalSubscriber signalSubscriber) {
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        container.addMessageListener(signalSubscriber, new PatternTopic("signals"));
        return container;
    }
}

