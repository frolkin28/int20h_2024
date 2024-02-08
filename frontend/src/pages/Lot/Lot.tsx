import React from 'react';
import { useParams } from 'react-router-dom';

export const LotPage = () => {
  const { lotId } = useParams()

  return <h1>Lot with ID {lotId}</h1>
}
