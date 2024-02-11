import { useParams } from "react-router-dom";

import { BetsList } from "../../components";

export const LotPage = () => {
  const { lotId } = useParams<{ lotId: string }>();

  return (
    <div>
      <div>
        <h1>Lot with ID {lotId}</h1>
      </div>
      <BetsList lotId={Number(lotId)} />
    </div>
  );
};
