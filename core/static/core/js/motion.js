(function () {
    "use strict";

    const MOTION_CONFIG = Object.freeze({
        durations: Object.freeze({
            standard: 1.0,
            hero: 1.25,
            compact: 0.8,
            heroCompact: 0.95,
        }),
        distances: Object.freeze({
            standard: 16,
            compact: 10,
            heroVisualX: 18,
        }),
        staggers: Object.freeze({
            standard: 0.28,
            hero: 0.22,
        }),
        ease: "power2.out",
        media: Object.freeze({
            wide: "(min-width: 992px)",
            compact: "(max-width: 991px)",
            reduced: "(prefers-reduced-motion: reduce)",
        }),
        scroll: Object.freeze({
            wideSectionStart: "top 82%",
            wideGridStart: "top 70%",
            compactSectionStart: "top 88%",
            compactGridStart: "top 78%",
            once: true,
        }),
        clearProperties: Object.freeze([
            "opacity",
            "transform",
            "visibility",
        ]),
    });

    const heroRoot = document.querySelector('[data-motion-root="hero"]');
    const heroCopyElements = heroRoot
        ? Array.from(
            heroRoot.querySelectorAll('[data-motion="hero-copy"]')
        )
        : [];
    const heroVisualElement = heroRoot
        ? heroRoot.querySelector('[data-motion="hero-visual"]')
        : null;
    const projectListRoots = Array.from(
        document.querySelectorAll('[data-motion-root="project-list"]')
    );
    const caseStudySections = Array.from(
        document.querySelectorAll('[data-motion="case-study-section"]')
    );
    const projectListElements = projectListRoots.flatMap((root) => [
        root.querySelector('[data-motion="section-intro"]'),
        ...root.querySelectorAll('[data-motion="project-card"]'),
    ]).filter(Boolean);
    const motionElements = [
        ...heroCopyElements,
        ...(heroVisualElement ? [heroVisualElement] : []),
        ...projectListElements,
        ...caseStudySections,
    ];

    function clearMotionStyles(elements) {
        elements.forEach((element) => {
            MOTION_CONFIG.clearProperties.forEach((property) => {
                element.style.removeProperty(property);
            });
        });
    }

    if (motionElements.length === 0) {
        return;
    }

    function getResponsiveSettings(isWide) {
        return {
            duration: isWide
                ? MOTION_CONFIG.durations.standard
                : MOTION_CONFIG.durations.compact,
            distance: isWide
                ? MOTION_CONFIG.distances.standard
                : MOTION_CONFIG.distances.compact,
            sectionStart: isWide
                ? MOTION_CONFIG.scroll.wideSectionStart
                : MOTION_CONFIG.scroll.compactSectionStart,
            gridStart: isWide
                ? MOTION_CONFIG.scroll.wideGridStart
                : MOTION_CONFIG.scroll.compactGridStart,
        };
    }

    function createHeroTimeline(gsap, isWide) {
        if (
            !heroRoot
            || heroCopyElements.length === 0
            || !heroVisualElement
        ) {
            return null;
        }

        const duration = isWide
            ? MOTION_CONFIG.durations.hero
            : MOTION_CONFIG.durations.heroCompact;
        const distance = isWide
            ? MOTION_CONFIG.distances.standard
            : MOTION_CONFIG.distances.compact;
        const visualStart = isWide
            ? {
                opacity: 0,
                x: MOTION_CONFIG.distances.heroVisualX,
                y: 0,
            }
            : {
                opacity: 0,
                x: 0,
                y: MOTION_CONFIG.distances.compact,
            };
        const heroElements = [...heroCopyElements, heroVisualElement];
        const timeline = gsap.timeline({
            onComplete: () => clearMotionStyles(heroElements),
        });

        timeline.fromTo(
            heroCopyElements,
            {
                opacity: 0,
                y: distance,
            },
            {
                opacity: 1,
                y: 0,
                duration,
                stagger: MOTION_CONFIG.staggers.hero,
                ease: MOTION_CONFIG.ease,
                immediateRender: false,
            },
            0
        );

        timeline.fromTo(
            heroVisualElement,
            visualStart,
            {
                opacity: 1,
                x: 0,
                y: 0,
                duration,
                ease: MOTION_CONFIG.ease,
                immediateRender: false,
            },
            0
        );

        return timeline;
    }

    // ScrollTrigger functionality
    function createSectionReveal(gsap, element, settings) {
        return gsap.fromTo(
            element,
            {
                opacity: 0,
                y: settings.distance,
            },
            {
                opacity: 1,
                y: 0,
                duration: settings.duration,
                ease: MOTION_CONFIG.ease,
                immediateRender: false,
                onComplete: () => clearMotionStyles([element]),
                scrollTrigger: {
                    trigger: element,
                    start: settings.sectionStart,
                    once: MOTION_CONFIG.scroll.once,
                },
            }
        );
    }

    function createProjectGridReveal(gsap, root, settings) {
        const gridElement = root.querySelector(
            '[data-motion="project-grid"]'
        );

        if (!gridElement) {
            return null;
        }

        const cardElements = Array.from(
            gridElement.querySelectorAll('[data-motion="project-card"]')
        );

        if (cardElements.length === 0) {
            return null;
        }

        const timeline = gsap.timeline({
            onComplete: () => clearMotionStyles(cardElements),
            scrollTrigger: {
                trigger: gridElement,
                start: settings.gridStart,
                once: MOTION_CONFIG.scroll.once,
            },
        });

        timeline.fromTo(
            cardElements,
            {
                opacity: 0,
                y: settings.distance,
            },
            {
                opacity: 1,
                y: 0,
                duration: settings.duration,
                ease: MOTION_CONFIG.ease,
                stagger: {
                    each: MOTION_CONFIG.staggers.standard,
                    from: "start",
                },
                immediateRender: false,
            }
        );

        return timeline;
    }

    function createScrollReveals(gsap, settings) {
        const animations = [];

        projectListRoots.forEach((root) => {
            const introElement = root.querySelector(
                '[data-motion="section-intro"]'
            );

            if (introElement) {
                animations.push(
                    createSectionReveal(gsap, introElement, settings)
                );
            }

            const gridTimeline = createProjectGridReveal(
                gsap,
                root,
                settings
            );

            if (gridTimeline) {
                animations.push(gridTimeline);
            }
        });

        caseStudySections.forEach((section) => {
            animations.push(
                createSectionReveal(gsap, section, settings)
            );
        });

        return animations;
    }

    const gsap = window.gsap;

    if (
        !gsap
        || typeof gsap.timeline !== "function"
        || typeof gsap.matchMedia !== "function"
    ) {
        clearMotionStyles(motionElements);
        return;
    }

    let scrollTriggerAvailable = false;

    if (
        window.ScrollTrigger
        && typeof gsap.registerPlugin === "function"
    ) {
        try {
            gsap.registerPlugin(window.ScrollTrigger);
            scrollTriggerAvailable = true;
        } catch (error) {
            scrollTriggerAvailable = false;
        }
    }

    try {
        const motionMedia = gsap.matchMedia();

        motionMedia.add(
            {
                isWide: MOTION_CONFIG.media.wide,
                isCompact: MOTION_CONFIG.media.compact,
                reduceMotion: MOTION_CONFIG.media.reduced,
            },
            (context) => {
                const { isWide, reduceMotion } = context.conditions;
                const animations = [];

                clearMotionStyles(motionElements);

                if (reduceMotion) {
                    return () => clearMotionStyles(motionElements);
                }

                const heroTimeline = createHeroTimeline(gsap, isWide);

                if (heroTimeline) {
                    animations.push(heroTimeline);
                }

                if (scrollTriggerAvailable) {
                    const settings = getResponsiveSettings(isWide);
                    animations.push(
                        ...createScrollReveals(gsap, settings)
                    );
                }

                return () => {
                    animations.forEach((animation) => animation.kill());
                    clearMotionStyles(motionElements);
                };
            }
        );
    } catch (error) {
        clearMotionStyles(motionElements);
    }
})();
