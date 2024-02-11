import { useState, useCallback, useRef, useEffect, useContext } from "react";
import { Manager, Socket } from "socket.io-client";

import { Bet } from "../types";
import { registerBaseListeners, AuctionEvents } from "../lib/ws";
import { AuthContext } from "../AuthContext";

interface AuctionState {
  bets: Bet[];
  makeBet: (amount: number) => void;
}

export const useAuction: (lotID: number) => AuctionState = (lotID) => {
  const [bets, setBets] = useState<Bet[]>([]);
  const ws = useRef<Socket | null>(null);
  const { token } = useContext(AuthContext);

  const joinAuction = useCallback(
    (lotID: number) => {
      ws.current?.emit("join_auction", { lot_id: lotID });
    },
    [ws]
  );

  const onConnect = useCallback(() => {
    joinAuction(lotID);
  }, [lotID, joinAuction]);

  const onReconnect = useCallback(() => {
    setBets([]);
    joinAuction(lotID);
  }, [lotID, joinAuction]);

  useEffect(() => {
    if (!process.env.REACT_APP_BASE_URL) {
      throw Error("Base url is not specified");
    }
    const manager = new Manager(process.env.REACT_APP_BASE_URL, {
      reconnectionDelayMax: 1000,
    });
    ws.current = manager.socket("/bets");

    const wsCurrent = ws.current;

    registerBaseListeners(wsCurrent, onConnect, onReconnect);

    wsCurrent.on(AuctionEvents.BET_CREATION_SUCCESS, (data) => {
      alert(data.message);
    });

    wsCurrent.on(AuctionEvents.BETS_LOG_UPDATE, (data) => {
      setBets((prevState) => {
        return [...prevState, ...data.bets];
      });
    });

    return () => {
      wsCurrent.disconnect();
    };
  }, []);

  const makeBet = useCallback(
    (amount: number) => {
      if (!ws.current) return;

      ws.current.emit(AuctionEvents.BET, {
        lot_id: lotID,
        amount: amount,
        access_token: token,
      });
    },
    [lotID, token, ws]
  );

  return { bets, makeBet };
};
