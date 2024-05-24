type Props = {
  title: string
  url: string
}

export default function AudioItem({ title, url }: Props) {
  return (
    <div className="grid grid-cols-5 items-center gap-2 w-full">
      <p className="font-medium">🔊{title}</p>
      <audio controls src={url} autoPlay={false} className="col-span-4 w-full"></audio>
    </div>
  )
}
