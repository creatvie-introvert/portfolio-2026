(function () {
    "use strict";

    const MOTION_CONFIG = Object.freeze({
        durations: Object.freeze({
            standard: 0.55,
            hero: 0.7,
            compact: 0.4,
        }),
        distances: Object.freeze({
            standard: 16,
            compact: 10,
            heroVisualX: 18,
        }),
        staggers: Object.freeze({
            standard: 0.08,
            hero: 0.1,
        }),
        ease: "power2.out",
        media: Object.freeze({
            wide: "(min-width: 992px)",
            compact: "(max-width: 991px)",
            reduced: "(prefers-reduced-motion: reduce)",
        }),
        clearProperties: Object.freeze([
            "opacity",
            "transform",
            "visibility",
        ]),
    });

    const heroRoot = document.querySelector('[data-motion-root="hero"]');

    if (!heroRoot) {
        return;
    }

    const copyElements = Array.from(
        heroRoot.querySelectorAll('[data-motion="hero-copy"]')
    );
    const visualElement = heroRoot.querySelector(
        '[data-motion="hero-visual"]'
    );
    const motionElements = visualElement
        ? [...copyElements, visualElement]
        : copyElements;

    function clearMotionStyles(elements) {
        elements.forEach((element) => {
            MOTION_CONFIG.clearProperties.forEach((property) => {
                element.style.removeProperty(property);
            });
        });
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

    try {
        if (
            window.ScrollTrigger
            && typeof gsap.registerPlugin === "function"
        ) {
            gsap.registerPlugin(window.ScrollTrigger);
        }

        const motionMedia = gsap.matchMedia();

        motionMedia.add(
            {
                isWide: MOTION_CONFIG.media.wide,
                isCompact: MOTION_CONFIG.media.compact,
                reduceMotion: MOTION_CONFIG.media.reduced,
            },
            (context) => {
                const { isWide, reduceMotion } = context.conditions;

                clearMotionStyles(motionElements);

                if (
                    reduceMotion
                    || copyElements.length === 0
                    || !visualElement
                ) {
                    return () => clearMotionStyles(motionElements);
                }

                const duration = isWide
                    ? MOTION_CONFIG.durations.hero
                    : MOTION_CONFIG.durations.compact;
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

                const timeline = gsap.timeline({
                    onComplete: () => clearMotionStyles(motionElements),
                });

                timeline.fromTo(
                    copyElements,
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
                    visualElement,
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

                return () => {
                    timeline.kill();
                    clearMotionStyles(motionElements);
                };
            }
        );
    } catch (error) {
        clearMotionStyles(motionElements);
    }
})();
