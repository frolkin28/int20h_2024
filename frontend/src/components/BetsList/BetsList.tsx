import { useState } from "react";
import { useAuction, useAuth } from "../../hooks";
import { BetItem } from "./views/BetItem";

interface BetsListProps {
  lotId: number;
}

export const BetsList = ({ lotId }: BetsListProps) => {
  const { bets, makeBet } = useAuction(lotId);
  const [newBetAmount, setNewBetAmount] = useState("");
  const { isSignedIn } = useAuth();

  const handleMakeBet = (e: React.FormEvent) => {
    e.preventDefault();

    if (!isSignedIn) {
      return alert("Необхідно авторизуватись")
    }

    const amount = newBetAmount?.trim()

    if (!amount || amount === "") {
      return alert("Введіть суму")
    }

    const bet = parseFloat(newBetAmount);
    if (bet) {
      makeBet(bet);
      setNewBetAmount("");
    } else {
      alert("Це невалідна сума");
    }
  };

  return (
    <div>
      <div>
        <h3>Поточні ставки</h3>
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

          <button type="submit">
            Підняти
          </button>
        </form>
      </div>
    </div>
  );
};
