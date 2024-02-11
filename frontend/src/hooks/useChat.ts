import { useState, useCallback, useRef, useEffect } from "react";
import { Manager, Socket } from "socket.io-client";

import { Message } from "../types";
import { registerBaseListeners, ChatEvents } from "../lib/ws";
import { useAuth } from "./useAuth";

interface AuctionState {
  messages: Message[];
  createMessage: (message: string) => void;
}

export const useChat: (lotID: number) => AuctionState = (lotID) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const ws = useRef<Socket | null>(null);
  const { token } = useAuth();

  const joinChat = useCallback(
    (lotID: number) => {
      ws.current?.emit(ChatEvents.JOIN_CHAT, { lot_id: lotID });
    },
    [ws]
  );

  const onConnect = useCallback(() => {
    joinChat(lotID);
  }, [lotID, joinChat]);

  const onReconnect = useCallback(() => {
    setMessages([]);
    joinChat(lotID);
  }, [lotID, joinChat]);

  useEffect(() => {
    if (!process.env.REACT_APP_BASE_URL) {
      throw Error("Base url is not specified");
    }
    const manager = new Manager(process.env.REACT_APP_BASE_URL, {
      reconnectionDelayMax: 1000,
    });
    ws.current = manager.socket("/chat");

    const wsCurrent = ws.current;

    registerBaseListeners(wsCurrent, onConnect, onReconnect);

    wsCurrent.on(ChatEvents.CHAT_UPDATE, (data) => {
      setMessages((prevState) => {
        return [...prevState, ...data.messages];
      });
    });

    return () => {
      wsCurrent.disconnect();
    };
  }, []);

  const createMessage = useCallback(
    (message: string) => {
      if (!(ws.current && message)) return;

      ws.current.emit(ChatEvents.NEW_MESSAGE, {
        message,
        lot_id: lotID,
        access_token: token,
      });
    },
    [lotID, token, ws]
  );

  return { messages, createMessage };
};
