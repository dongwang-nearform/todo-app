import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { CopyReviewPage } from './features/copy/CopyReviewPage.tsx'
import { ListPage } from './features/lists/ListPage.tsx'
import { ListsPage } from './features/lists/ListsPage.tsx'
import { NotDonePage } from './features/not-done/NotDonePage.tsx'
import { PeriodPage } from './features/period/PeriodPage.tsx'
import { TodayPage } from './features/today/TodayPage.tsx'
import { Shell } from './layout/Shell.tsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Shell />}>
          <Route index element={<TodayPage />} />
          <Route path="not-done" element={<NotDonePage />} />
          <Route path="lists" element={<ListsPage />} />
          <Route path="lists/:listId" element={<ListPage />} />
          <Route path="period" element={<PeriodPage />} />
          <Route path="copies/:copyId" element={<CopyReviewPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
