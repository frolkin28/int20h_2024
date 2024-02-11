import { Bet } from "../../../types";
import "./style.css";

interface BetListItemProps {
  bet: Pick<Bet, "creation_date" | "amount" | "author">;
}

export const BetItem: React.FC<BetListItemProps> = ({ bet }) => {
  const { creation_date, amount, author } = bet;

  return (
    <li>
      <div>
        <p>Date: {creation_date}</p>
        <p>Amount: {amount} грн.</p>
        <span className="bet-author-fullname">
          {author.first_name} {author.last_name}
        </span>
        <span className="bet-author-email">{author.email}</span>
      </div>
    </li>
  );
};
