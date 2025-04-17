package signal_trader.simulator.model;

import jakarta.persistence.*;
import lombok.*;

@Data
@Entity
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "trades")
public class Trade {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String symbol;
    private String type; // BUY or SELL
    private double entryPrice;
    private double exitPrice;
    private double pnl;
    private double confidence;
    private String reason;
    private long timestamp;

}
