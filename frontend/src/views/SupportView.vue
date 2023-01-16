<script setup lang="ts">
import TheSupport from "@/components/TheSupport.vue";
</script>

<template>
  <div class="about">
    <div>
      <TheSupport />
    </div>
  </div>
</template>

<style>
/*
em - от текущего шоифта
% - от родительской ширины
rem - от стиля html
vw – 1% ширины окна
vh – 1% высоты окна
vmin – наименьшее из (vw, vh), в IE9 обозначается vm
vmax – наибольшее из (vw, vh)
*/

div .about {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

h2 {
  text-align: center;
  font-size: 1.4em;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
}
</style>
