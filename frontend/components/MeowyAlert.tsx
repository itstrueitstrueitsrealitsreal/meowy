import { PiCatDuotone } from "react-icons/pi";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export function MeowyAlert() {
  return (
    <Alert>
      <PiCatDuotone className="h-4 w-4" />
      <AlertTitle>Hi, I&apos;m Meowy!</AlertTitle>
      <AlertDescription>
        I&apos;m part of the Cat Delivery Network, and it&apos;s my job to cheer
        people up! Let me know which breed of cat and how many of them you want
        to see to get started! Meow :3
      </AlertDescription>
    </Alert>
  );
}
