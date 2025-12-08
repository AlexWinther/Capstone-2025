import * as React from "react";
import { cn } from "@/lib/utils";

export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <select
        className={cn(
          "flex w-full rounded-xl border-none bg-white/70 px-4 py-3 text-base text-text-primary shadow-md transition-all appearance-none cursor-pointer",
          "focus:bg-white/95 focus:shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/20",
          "hover:bg-white/85 hover:shadow-lg",
          className
        )}
        ref={ref}
        {...props}
      >
        {children}
      </select>
    );
  }
);
Select.displayName = "Select";

export { Select };

