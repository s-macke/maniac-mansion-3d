import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'Maniac Mansion · Entrance & landing',
  description: 'Explore the entrance hall and connected upstairs balcony in first person. A 3D interpretation of the original EGA artwork.',
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
