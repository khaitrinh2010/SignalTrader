package signal_trader.simulator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import signal_trader.simulator.model.Trade;

@Repository
public interface TradeRepository extends JpaRepository<Trade, Long> {
}
