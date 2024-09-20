import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";
import Autoplay from "embla-carousel-autoplay";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel";

interface ImageGalleryProps {
  imageUrls: string[];
}

export function ImageGallery({ imageUrls }: ImageGalleryProps) {
  const [api, setApi] = React.useState<CarouselApi | null>(null);
  const [current, setCurrent] = React.useState(1);
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    if (!api) return;

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);

    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);

  return (
    <div className="flex flex-col items-center justify-center">
      <Carousel
        setApi={setApi}
        plugins={[
          Autoplay({
            delay: 3000,
            stopOnInteraction: true,
          }),
        ]}
        className="w-full max-w-xs"
      >
        <CarouselContent>
          {imageUrls.map((url, index) => (
            <CarouselItem key={index}>
              <div className="p-1">
                <Card>
                  <CardContent className="flex aspect-square items-center justify-center p-6">
                    <Image
                      src={url}
                      alt={`Cat ${index + 1}`}
                      width={300}
                      height={300}
                      className="size-full rounded-lg object-cover"
                    />
                  </CardContent>
                </Card>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>

      <div className="py-2 text-center text-sm text-muted-foreground">
        Cat {current} of {count}
      </div>
    </div>
  );
}
