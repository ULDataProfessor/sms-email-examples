import React from 'react';
import EventList from '../components/EventList';
import DiscountBanner from '../components/DiscountBanner';
import AdSlot from '../components/AdSlot';

export default function ClubDetail() {
  return (
    <div>
      <h2>Club Detail</h2>
      <DiscountBanner />
      <EventList />
      <AdSlot />
    </div>
  );
}
