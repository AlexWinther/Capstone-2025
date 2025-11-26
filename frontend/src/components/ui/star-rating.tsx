import { cn } from "@/lib/utils";

interface StarRatingProps {
  value: number; // 0-5
  onChange?: (value: number) => void;
  readonly?: boolean;
  className?: string;
}

export const StarRating = ({ value, onChange, readonly = false, className }: StarRatingProps) => {
  const handleClick = (newValue: number) => {
    if (!readonly && onChange) {
      onChange(newValue);
    }
  };

  return (
    <div className={cn("flex gap-1", className)}>
      {[1, 2, 3, 4, 5].map((starValue) => (
        <button
          key={starValue}
          type="button"
          onClick={() => handleClick(starValue)}
          disabled={readonly}
          className={cn(
            "text-xl leading-none transition-colors",
            starValue <= value
              ? "text-yellow-400"
              : "text-gray-300",
            !readonly && "cursor-pointer hover:text-yellow-300",
            readonly && "cursor-default"
          )}
          aria-label={`Rate ${starValue} out of 5`}
        >
          {starValue <= value ? "★" : "☆"}
        </button>
      ))}
    </div>
  );
};

