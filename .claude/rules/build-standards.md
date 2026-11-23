# Supercraft Elementor & Novamira Build Standards

## 1. Build Order
- Set up the design system first. Show colour swatches and live font-pairing examples, and get approval before building.
- Save the design system as the site's global colours, global typography, and boxed width. Then build against it.
- Work section by section, and examine every reference page before building.
- Cut a placeholder logo from the brand assets and swap in the real one later.
- Use the lowest build tier that works: native Elementor, then custom CSS or JS, then a custom component. Ask before building a custom plugin.

## 2. Global and Reusable
- Every colour and text style must reference the global colours and typography presets. Don't use hard-coded hex values or per-widget custom typography.
- Hard-code only what globals can't express, such as semi-transparent fills and shadows.
- Keep the preset set small and named by role (`H1`, `H2`, `Body`, `Caption`, `Eyebrow`, `Button`, etc.). Merge near-duplicate sizes instead of adding one preset per size.
- Set the body font globally.
- Edit the kit by merging into its settings. Never replace them.
- If you generate the page from code, run a step before publishing that converts literals into global references.

## 3. Styling
- Style with native Elementor controls. Use custom CSS only where no control exists (such as backdrop blur, looping marquees, or inline highlights), and keep it minimal and commented.
- Containers use `margin` and `padding`; widgets use `_margin` and `_padding`. Using the wrong one fails silently, so confirm that overlaps and offsets applied.
- Set the kit's default container padding to `0`, otherwise it stacks at every nesting level.
- Percentage widths plus gaps must total under `100%`, or the row wraps.
- Zero the last paragraph's bottom margin once, globally, so container gaps control the spacing.
- Set heading size, line height, and tracking explicitly, with tablet and mobile sizes.
- Use explicit line breaks sparingly, and hide them on mobile so the text can flow.
- Keep the approved palette and fonts fixed unless the user asks to change them.

## 4. Assets
- Generate bespoke images with the image tool and review each one visually before uploading.
- Brief image generation with the layout in mind (for example, a clear side for headline text).
- Cut out product shots with background removal and use the transparent file.
- Upload through Novamira, import into the media library, and record the media IDs in one shared helper file.

## 5. Motion
- Use the animation plugin for entrance and idle effects, and Elementor Pro motion effects for parallax.
- Disable parallax on mobile.
- Check how motion actually behaves (for example, loops and scroll effects). Confirming the setting exists isn't enough.

## 6. Verification
- Set the preview viewport explicitly (desktop width, then `375px` mobile, then tablet) before judging a layout.
- Speed up animations before taking screenshots, for example with `gsap.globalTimeline.timeScale(50)`.
- Measure instead of guessing. Read computed margins, sizes, and transforms in the page to find the cause of spacing problems.
- Check for horizontal overflow at `375px` and open the Elementor editor at the end.
- Compare computed values before and after any bulk change (such as a global conversion) to confirm the look is unchanged.
- Reset the viewport to desktop when you finish testing.

## 7. Working with the User
- If a request is ambiguous, work out what they mean before changing anything.
- When asked for options or suggestions, list them and leave the page alone until they choose.
- Keep pages as drafts until the user says to publish.
- Report what you couldn't verify.
