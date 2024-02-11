import { useState, useEffect, useRef, useContext } from "react";
import { Button } from "../Buttons/Button";
import { TextInput } from "../Input/TextInput";
import { useChat } from "../../hooks/useChat";
import { AuthContext } from "../../AuthContext";
import styles from "./Chat.module.css"

export const Chat = ({ lotId }: { lotId: number }) => {
  const [inputMessage, setInputMessage] = useState<string>("");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { messages, createMessage } = useChat(lotId);
  const { isSignedIn } = useContext(AuthContext);

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
    if (!isSignedIn) {
      return alert("Необхідно авторизуватися")
    }

    const message = inputMessage?.trim()

    if(!message || message === "") {
      return alert("Введіть повідомлення")
    }

    createMessage(inputMessage);
    setInputMessage("");
  };

  return (
    <div>
      <h3>Чат аукціону</h3>
      <div className={styles.chatWrapper} ref={chatContainerRef}>
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
          text="Відправити"
        />
      </div>
    </div>
  );
};

export default Chat;
