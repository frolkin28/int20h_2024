export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Bet {
  id: number;
  lot_id: number;
  amount: number;
  creation_date: number;
  author: User;
}

export interface Message {
  id: number;
  content: string;
  lot_id: string;
  creation_date: string;
  author: User;
}

export interface Lot {
  lot_name: string;
  description: string;
  pictures: string[];
  end_date: string;
  creation_date: string;
  author: User;
}

export interface LotPreview {
  lot_id: number;
  lot_name: string;
  description: string;
  picture: string;
  end_date: string;
  price: number;
}