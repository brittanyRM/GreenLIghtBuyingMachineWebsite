/* Nav order is defined here rather than in the CMS so editors can't
   accidentally break routing. Labels are editable per page. */
export const NAV = [
  { href: "/", label: "Home" },
  { href: "/how-it-works", label: "Build with us" },
  { href: "/for-buyers", label: "Buy a property" },
  { href: "/homes", label: "Homes we've built" },
  { href: "/faq", label: "FAQ" },
  { href: "/about", label: "About" },
];

export const HOMES = [
  ["kitchen-navy", "Shared kitchen"],
  ["common-green", "Common area"],
  ["kitchen-green", "Shared kitchen"],
  ["dining-bar", "Dining and living"],
  ["living-open", "Living room"],
  ["common-seating", "Common seating"],
  ["bedroom-eight", "Room 8"],
  ["bedroom-yellow", "Bedroom"],
  ["bedroom-desert", "Bedroom"],
  ["bedroom-two", "Bedroom"],
  ["harmony-kitchen", "Harmony · kitchen"],
  ["harmony-common", "Harmony · common area"],
  ["pepper-kitchen", "Pepper · kitchen"],
  ["pepper-common", "Pepper · common area"],
  ["howe-kitchen", "Howe · kitchen"],
  ["howe-bedroom", "Howe · bedroom"],
  ["laundry", "Shared laundry"],
] as const;

export const PLANS = [
  ["plan-ash", "Ash · 8 bedrooms, 7 bathrooms"],
  ["plan-colors", "Ten bedrooms named by colour"],
  ["plan-ten-room", "Ten-room conversion, 2,011 sq ft"],
  ["plan-harmony", "Harmony · 2,074 sq ft"],
  ["plan-rooms", "Ten bedrooms, 1,926 sq ft"],
  ["plan-pepper", "Pepper · 1,863 sq ft"],
] as const;
