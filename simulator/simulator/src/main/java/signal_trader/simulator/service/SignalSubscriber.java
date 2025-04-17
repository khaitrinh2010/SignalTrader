package signal_trader.simulator.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.data.redis.connection.Message;
import org.springframework.stereotype.Service;
import signal_trader.simulator.model.Signal;

import com.fasterxml.jackson.databind.ObjectMapper;

@Service
@RequiredArgsConstructor
public class SignalSubscriber implements MessageListener{
    private final ObjectMapper mapper = new ObjectMapper();

    private final TradeSimulatorService tradeSimulatorService;
    @Override
    public void onMessage(Message message, byte[] pattern) {
        try{
            String json = new String(message.getBody());
            Signal signal = mapper.readValue(json, Signal.class);
            System.out.println("Received signal: " + signal.getSymbol() + ", Type: " + signal.getType() + ", Confidence: " + signal.getConfidence() + ", Reason: " + signal.getReason() + ", Timestamp: " + signal.getTimestamp());
            tradeSimulatorService.simulateTrade(signal);
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }
}
