package signal_trader.simulator.model;

import lombok.Data;

@Data
public class Signal {
    private String symbol;
    private String type;
    private double confidence;
    private String reason;
    private long timestamp;
}
