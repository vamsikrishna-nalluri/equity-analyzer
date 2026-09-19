# Version-1:
```
<role>
You are an experienced React developer, your goal is to create a react component.
</role>

<context>
1. libraries - React version: 19.3.0, vite : 8.3.0, vitest : 5.0.0, axios : 1.20.0
2. build a standalone components.
3. use typescript to build the components.
4. use UI library tailwindcss : 4.3.3, to build the html pages.
</context>

<goal>
1. Build a Component which can get the fundamental details of a stock and show it on a page.
2. The screen should have a input text , which takes the stock name and fetches the stock fundamental details to show on the page.
3. Make sure to add all necessary accessibility properties to the UI component.
4. The component must be responsive across mobile, tablet, and desktop screen sizes.
5. Maintain a proper package structure, add any custome packages/folders based on the functionality.
6. Make sure appropriate file names are used, which identifies it's functionality.
5. Always use the css variable, if defined at the project level to get the same UX design for each component.
</goal>

<expected_output>
1. component typescript file- a `.tsx` file
2. a `.html` file should be created.
3. a `.scss` file should be created
4. make sure the tests are created to verify the functionality. Always create the tests once the implementation complete(verify the source files are created).
</expected_output>

<example>
folder structure:
    src
        - stock
            - fundamentals
                - stockFundamentals.tsx
                - stockFundamentals.test.tsx
                - stock.html
                - stock.scss
</example>
```

# Version-2
```
<role>
You are a senior React and TypeScript frontend developer experienced in building
production-grade, accessible and responsive web applications.
</role>

<context>
1. React version: 19.3.0
2. Vite version: 8.3.0
3. Vitest version: 5.0.0
4. Axios version: 1.20.0
5. TailwindCSS version: 4.3.3
6. Use TypeScript.
7. Follow a feature-based project structure.
</context>

<goal>
Build a Stock Fundamentals component.

The component must:

1. Provide an input field where the user enters a stock ticker.
2. Fetch stock fundamental information from the provided API.
3. Display the returned fundamental information.
4. Handle initial, loading, success, empty and error states.
5. Be responsive across mobile, tablet and desktop.
6. Follow accessibility best practices.
7. Use existing project-level CSS variables when they are available.
8. Use meaningful file and folder names.
9. Keep responsibilities separated between UI, API access and data types.
</goal>

<api_contract>
GET /api/v1/stock/{ticker}

Example response:

{
  "ticker": "INFY",
  "fundamentals": {
    "price": 1520.50,
    "marketCap": 650000000000,
    "peRatio": 24.5,
    "eps": 62.1
  }
}
</api_contract>

<accessibility>
1. Use semantic HTML.
2. Every form control must have an accessible label.
3. Support keyboard navigation.
4. Provide visible focus states.
5. Use ARIA attributes only where necessary.
6. Provide accessible loading and error messages.
</accessibility>

<responsive_design>
1. Support mobile, tablet and desktop.
2. Use Tailwind responsive utilities.
3. Avoid unnecessary fixed positioning.
4. Avoid horizontal scrolling at normal viewport sizes.
</responsive_design>

<testing>
Create tests after the implementation is complete.

Tests should verify:

1. Component renders correctly.
2. User can enter a ticker.
3. API request is triggered with the entered ticker.
4. Loading state is displayed.
5. Successful response is displayed.
6. API error is handled correctly.
7. Empty input is handled correctly.
8. Accessibility-related behaviour is verified where practical.
</testing>

<project_structure>
Use the following structure as a guideline:

src/
├── features/
│   └── stock/
│       └── fundamentals/
│           ├── StockFundamentals.tsx
│           ├── StockFundamentals.test.tsx
│           ├── stockApi.ts
│           └── types.ts
</project_structure>

<constraints>
1. Do not invent API endpoints or response fields.
2. Do not introduce dependencies that are not listed above unless explicitly justified.
3. Reuse existing project-level CSS variables when available.
4. Do not make assumptions about unavailable project configuration.
5. If any required information is missing, clearly identify it before implementing.
</constraints>

<expected_output>
1. Show the proposed folder structure.
2. Show each source file with its complete contents.
3. Show the test files with their complete contents.
4. Explain the key implementation decisions.
5. List any assumptions or missing information.
</expected_output>
```

## Issues identified:
- Invented the API endpoint and response model because no API contract was provided.
- Created CSS variables instead of relying only on existing project variables.
- Test coverage was incomplete.
- API logic was tightly coupled to the UI component.
- Used catch (err: any) rather than safer unknown/Axios - error handling.

## Key learning:
- AI can generate a good initial UI implementation quickly, but the developer must validate API contracts, architecture, accessibility, testing, and project conventions. Missing context can lead to hallucinated implementation details.