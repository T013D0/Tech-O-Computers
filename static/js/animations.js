$(document).ready(() => {
  const $cards = [...$(".card-product")];

  console.log($cards);

  gsap.from($cards, {
    opacity: 0,
    y: 20,
    duration: 1,
    stagger: 0.1,
    ease: "power4.out",
    delay: 0.5,
  });
});
