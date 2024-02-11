import { useState, useEffect, useRef } from "react";
import { Button } from "../Buttons/Button";
import { TextInput } from "../Input/TextInput";
import { useChat } from "../../hooks/useChat";
import { useAuth } from "../../hooks";

export const Chat = ({ lotId }: { lotId: number }) => {
  const [inputMessage, setInputMessage] = useState<string>("");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { messages, createMessage } = useChat(lotId);
  const { isSignedIn } = useAuth();

  useEffect(() => {
    // Scroll to the bottom on new message
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleInputChange = (value: string) => {
    setInputMessage(value);
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() !== "") {
      createMessage(inputMessage);
      setInputMessage("");
    } else {
      alert("Невалідне повідомлення");
    }
  };

  return (
    <div>
      <h3>Чат аукціону</h3>
      <div
        style={{ height: "300px", overflowY: "auto" }}
        ref={chatContainerRef}
      >
        {messages.map((message) => (
          <div key={message.id}>
            <div>
              <strong>
                {message.author.first_name} {message.author.last_name}:
              </strong>
            </div>
            <div>
              <span>{message.content}</span>{" "}
              <span>
                <i>{message.creation_date}</i>
              </span>
            </div>
          </div>
        ))}
      </div>
      <div>
        <TextInput
          id="chat-message-input"
          value={inputMessage}
          onChange={handleInputChange}
          placeholder="Введіть повідомлення..."
        />
        <Button
          onClick={handleSendMessage}
          disabled={!(isSignedIn && inputMessage)}
          text={isSignedIn ? "Відправити" : "Необхідно авторизуватись"}
        />
      </div>
    </div>
  );
};

export default Chat;
