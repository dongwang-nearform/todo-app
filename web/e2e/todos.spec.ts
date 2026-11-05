import AxeBuilder from '@axe-core/playwright'
import { expect, request, test } from '@playwright/test'

// Every list these tests create starts with this prefix. The afterAll hook deletes them,
// so repeated runs leave the database as they found it.
const PREFIX = 'e2e '
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL ?? 'http://127.0.0.1:8080'

test.afterAll(async () => {
  const api = await request.newContext({ baseURL: BASE_URL })
  const response = await api.get('/api/lists')
  const lists = (await response.json()) as { id: number; name: string }[]
  for (const list of lists) {
    if (list.name.startsWith(PREFIX)) {
      await api.delete(`/api/lists/${list.id}`)
    }
  }
  await api.dispose()
})

test('shows the empty state for a day with no to-dos', async ({ page }) => {
  await page.goto('/?on_date=1999-01-01')
  await expect(page.getByText('No to-dos today.')).toBeVisible()
})

test('shows an error when a to-do is saved without a title', async ({ page }) => {
  const name = `${PREFIX}Err ${Date.now()}`
  await page.goto('/lists')
  await page.getByLabel('Name').fill(name)
  await page.getByRole('button', { name: 'Create a list' }).click()
  await page.getByRole('link', { name }).click()
  await page.getByRole('button', { name: 'Add to-do' }).click()
  await page.getByLabel('Priority').selectOption('3')
  await page.getByRole('button', { name: 'Save' }).click()
  await expect(page.getByRole('alert')).toContainText('Title is required')
})

test.describe.serial('create, complete, and delete', () => {
  const name = `${PREFIX}Life ${Date.now()}`
  const title = `Buy milk ${Date.now()}`

  test('creates a to-do', async ({ page }) => {
    await page.goto('/lists')
    await page.getByLabel('Name').fill(name)
    await page.getByRole('button', { name: 'Create a list' }).click()
    await page.getByRole('link', { name }).click()
    await page.getByRole('button', { name: 'Add to-do' }).click()
    await page.getByLabel('Title').fill(title)
    await page.getByLabel('Priority').selectOption('3')
    await page.getByRole('button', { name: 'Save' }).click()
    await expect(page.getByRole('button', { name: new RegExp(title) })).toBeVisible()
  })

  test('completes a to-do', async ({ page }) => {
    await page.goto('/lists')
    await page.getByRole('link', { name }).click()
    await page.getByRole('button', { name: new RegExp(title) }).click()
    await page.getByRole('button', { name: 'Mark done', exact: true }).click()
    await expect(page.getByText('State done')).toBeVisible()
  })

  test('deletes a to-do', async ({ page }) => {
    await page.goto('/lists')
    await page.getByRole('link', { name }).click()
    await page.getByRole('button', { name: new RegExp(title) }).click()
    await page.getByRole('button', { name: 'Delete', exact: true }).click()
    await expect(page.getByRole('button', { name: new RegExp(title) })).toHaveCount(0)
  })
})

test('has no critical WCAG AA violations on the main screens', async ({ page }) => {
  const paths = ['/?on_date=1999-01-01', '/lists', '/not-done', '/period']
  for (const path of paths) {
    await page.goto(path)
    await page.getByRole('heading', { level: 1 }).waitFor()
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze()
    const blocking = results.violations.filter(
      (item) => item.impact === 'critical' || item.impact === 'serious',
    )
    expect(blocking, `${path}: ${blocking.map((item) => item.id).join(', ')}`).toEqual([])
  }
})
