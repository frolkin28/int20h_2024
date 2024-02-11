import { Socket } from "socket.io-client";

export enum BaseEvents {
  JOIN_ERROR = "join_error",
  UNAUTHORIZED = "unauthorized",
  VALIDATION_ERROR = "validation_error",
}

export enum AuctionEvents {
  BETS_LOG_UPDATE = "bets_log_update",
  BET_CREATION_SUCCESS = "bet_creation_success",
  BET = "bet",
}

export enum ChatEvents {
  NEW_MESSAGE = "new_message",
  JOIN_CHAT = "join_chat",
  CHAT_UPDATE = "chat_update",
}

export function registerBaseListeners(
  socket: Socket,
  onConnect: () => void,
  onReconnect: () => void
) {
  socket.on("reconnect_attempt", (attempt) => {
    console.log(`Auction reconnection attempt: ${attempt}`);
  });

  socket.on("reconnect_error", (error) => {
    console.warn(error);
  });

  socket.on(BaseEvents.JOIN_ERROR, (data) => {
    alert(data.message);
  });

  socket.on(BaseEvents.UNAUTHORIZED, () => {
    alert("Авторизуйтесь для того, щоб зробити ставку");
  });

  socket.on(BaseEvents.VALIDATION_ERROR, (data) => {
    alert(JSON.stringify(data.message));
  });

  socket.on("connect", () => {
    console.log("Connected");
    onConnect();
  });

  socket.on("reconnect", (attempt) => {
    console.log(`Reconnected, attempts: ${attempt}`);
    onReconnect();
  });
}
