import { useEffect, useRef, type ReactNode } from 'react'

export function Workspace({
  title,
  editor,
  children,
}: {
  title: string
  editor: ReactNode | null
  children: ReactNode
}) {
  const heading = useRef<HTMLHeadingElement>(null)
  useEffect(() => {
    heading.current?.focus()
  }, [title])
  return (
    <div className={editor ? 'workspace editor-open' : 'workspace'}>
      <section className="reading">
        <h1 ref={heading} tabIndex={-1}>
          {title}
        </h1>
        <div className="list-body">{children}</div>
      </section>
      {editor ? <div className="editor">{editor}</div> : null}
    </div>
  )
}
