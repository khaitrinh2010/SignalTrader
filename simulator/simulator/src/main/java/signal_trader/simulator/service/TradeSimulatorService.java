package signal_trader.simulator.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import signal_trader.simulator.model.Signal;
import signal_trader.simulator.model.Trade;
import signal_trader.simulator.repository.TradeRepository;

@Service
@RequiredArgsConstructor
public class TradeSimulatorService {
    private final TradeRepository tradeRepository;
    private final StringRedisTemplate stringRedisTemplate;

    public void simulateTrade(Signal signal) {
        double entry = getCurrentMarketPrice(signal.getSymbol());
        double exit = simulateExitPrice(signal);
        double pnl = calculatePnL(signal.getType(), entry, exit);

        Trade trade = Trade.builder()
                .symbol(signal.getSymbol())
                .type(signal.getType())
                .entryPrice(entry)
                .exitPrice(exit)
                .pnl(pnl)
                .confidence(signal.getConfidence())
                .reason(signal.getReason())
                .timestamp(signal.getTimestamp())
                .build();

        tradeRepository.save(trade);
        System.out.println("[Simulator] Simulated Trade: " + trade);
    }

    private double getCurrentMarketPrice (String symbol) {
        try {
            String baseUrl = "https://api.binance.com/api/v3/ticker/price?symbol=" + symbol;
            RestTemplate restTemplate = new RestTemplate();
            String response = restTemplate.getForObject(baseUrl, String.class);

            ObjectMapper mapper = new ObjectMapper();
            JsonNode json = mapper.readTree(response);
            return json.has("price") ? json.get("price").asDouble() : 100.0;

        } catch (Exception e) {
            System.err.println("Failed to fetch market price from Binance for " + symbol + ": " + e.getMessage());
            return 100.0; // Fallback
        }
    }

    private double simulateExitPrice(Signal signal) {
        double base = getCurrentMarketPrice(signal.getSymbol());
        String type = signal.getType();
        switch (type) {
            case "BUY":
                return base * 1.001; // Price increases slightly
            case "SELL":
                return base * 0.999; // Price drops slightly
            case "ARBITRAGE_BUY":
                return base * 1.0008; // Price normalizes from undervaluation
            case "ARBITRAGE_SELL":
                return base * 0.9992; // Price normalizes from overvaluation
            case "MOMENTUM":
                return base * 1.002; // Price moves strongly in one direction
            default:
                return base;
        }
    }

    private double calculatePnL(String type, double entry, double exit) {
        return switch (type) {
            case "BUY", "ARBITRAGE_BUY", "MOMENTUM" -> exit - entry;
            case "SELL", "ARBITRAGE_SELL" -> entry - exit;
            default -> 0.0;
        };
    }
}
