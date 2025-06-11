import React, { useEffect } from 'react';

export default function NotificationBell() {
  useEffect(() => {
    if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
  }, []);

  const notify = () => {
    if (Notification.permission === 'granted') {
      new Notification('Club is open!');
    }
  };

  return (
    <button onClick={notify}>Notify me</button>
  );
}
