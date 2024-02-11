import { useState } from "react";
import { useAuction } from "../../hooks";
import { BetItem } from "./views/BetItem";

interface BetsListProps {
  lotId: number;
}

export const BetsList = ({ lotId }: BetsListProps) => {
  const { bets, makeBet } = useAuction(lotId);
  const [newBetAmount, setNewBetAmount] = useState("");

  const handleMakeBet = (e: React.FormEvent) => {
    e.preventDefault();
    if (newBetAmount.trim() !== "") {
      const bet = parseFloat(newBetAmount);
      if (bet) {
        makeBet(bet);
        setNewBetAmount("");
      } else {
        alert("Це невалідна сума");
      }
    }
  };

  return (
    <div>
      <div>
        <h3>Bets list</h3>
      </div>
      <div>
        <ul>
          {bets.map((bet) => (
            <BetItem key={bet.id} bet={bet} />
          ))}
        </ul>

        <form onSubmit={handleMakeBet}>
          <label>
            Зробити ставку:
            <input
              type="number"
              value={newBetAmount}
              onChange={(e) => setNewBetAmount(e.target.value)}
            />
          </label>
          <button type="submit">Place Bet</button>
        </form>
      </div>
    </div>
  );
};