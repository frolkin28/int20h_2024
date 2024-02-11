import { useState, useCallback, useRef, useEffect } from "react";
import { Manager, Socket } from "socket.io-client";

import { Bet } from "../types";
import { useAuth } from "./useAuth";

enum AuctionEvents {
  JOIN_ERROR = "join_error",
  UNAUTHORIZED = "unauthorized",
  VALIDATION_ERROR = "validation_error",
  BETS_LOG_UPDATE = "bets_log_update",
  BET_CREATION_SUCCESS = "bet_creation_success",
  BET = "bet",
}

interface AuctionState {
  bets: Bet[];
  makeBet: (amount: number) => void;
}

export const useAuction: (lotID: number) => AuctionState = (lotID) => {
  const [bets, setBets] = useState<Bet[]>([]);
  const ws = useRef<Socket | null>(null);
  const { token } = useAuth();

  const joinAuction = (lotID: number) => {
    ws.current?.emit("join_auction", { lot_id: lotID });
  };

  useEffect(() => {
    const manager = new Manager("ws://localhost:8080/ws", {
      reconnectionDelayMax: 1000,
    });
    ws.current = manager.socket("/bets");

    const wsCurrent = ws.current;

    wsCurrent.on("reconnect", (attempt) => {
      console.log(`Auction reconnected, attempts: ${attempt}`);
      setBets([]);
      joinAuction(lotID);
    });

    wsCurrent.on("reconnect_attempt", (attempt) => {
      console.log(`Auction reconnection attempt: ${attempt}`);
    });

    wsCurrent.on("reconnect_error", (error) => {
      console.warn(error);
    });

    wsCurrent.on(AuctionEvents.JOIN_ERROR, (data) => {
      alert(data.message);
    });

    wsCurrent.on(AuctionEvents.UNAUTHORIZED, () => {
      alert("Авторизуйтесь для того, щоб зробити ставку");
    });

    wsCurrent.on(AuctionEvents.VALIDATION_ERROR, (data) => {
      alert(data.message);
    });

    wsCurrent.on(AuctionEvents.BET_CREATION_SUCCESS, (data) => {
      alert(data.message);
    });

    wsCurrent.on(AuctionEvents.BETS_LOG_UPDATE, (data) => {
      setBets(data.bets);
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
    [lotID, token]
  );

  return { bets, makeBet };
};
