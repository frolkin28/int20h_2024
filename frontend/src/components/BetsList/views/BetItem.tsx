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
        <span className="bet-author-fullname">
          <strong>
            {author.first_name} {author.last_name}
          </strong>
        </span>
        <span className="bet-author-email">{author.email}</span>
        <p>
          Сума: {amount} грн. ({creation_date})
        </p>
      </div>
    </li>
  );
};
