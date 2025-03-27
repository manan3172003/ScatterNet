import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

export function Header({
  className,
  ...props
}: React.ComponentPropsWithoutRef<"div">) {
  return (
    <div className={cn("flex flex-col shadow-sm inset-0", className)} {...props}>
      <Card className="border-none bg-transparent">
        <CardHeader>
          <CardTitle className="text-6xl text-center font-bold text-primary">
            OnlyNodes
          </CardTitle>
        </CardHeader>
      </Card>
    </div>
  )
}