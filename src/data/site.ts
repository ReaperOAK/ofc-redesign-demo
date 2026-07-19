export const SITE = {
  name: "Overseas Food Consultants",
  legalName: "Overseas Food Consultants (OPC) Private Limited",
  tagline: "Your Source for Food Experts",
  subTagline: "Elevating Your Food Business",
  url: "https://ofc-redesign.vercel.app",
  address: "Haryana, India",
  registration:
    "Registered under the Companies Act 2013, Ministry of Corporate Affairs, Government of India",
  social: {
    linkedin: "https://www.linkedin.com/company/overseas-food-consultants",
    instagram: "https://www.instagram.com/overseas_foodconsultants",
    youtube: "https://www.youtube.com/@overseasfoodconsultants",
  },
} as const;

export const NAV = [
  { href: "/", label: "Home" },
  { href: "/consultancy", label: "Consultancy" },
  { href: "/case-studies", label: "Case Studies" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
] as const;
