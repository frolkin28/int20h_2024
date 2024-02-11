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
