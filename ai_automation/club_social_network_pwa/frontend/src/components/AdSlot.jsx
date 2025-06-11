import React from 'react';

export default function AdSlot({ admin }) {
  return (
    <div className="ad-slot">
      {admin ? 'Upload new ad here.' : 'Ad goes here.'}
    </div>
  );
}
