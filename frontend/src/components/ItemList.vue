<!-- 
 
The ItemList.vue component displays the scrollable list of grocery items.
Needs a bit more work, but wanted to get the scrolling list started :)


-->



<template>
  <div class="scroll-wrapper">
    <div class="scroll-container" ref="scrollContainer">
      <ul class="horizontal-list">
        <li 
          v-for="item in items" 
          :key="item.id"
          class="list-item"
        >
          <div class="item-content">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-type">{{ item.quantity }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref} from 'vue';

const props = defineProps({
  items: {
    type: Array,
    required: true,
  }
});

</script>

<style scoped>
.scroll-wrapper {
  position: relative;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.scroll-container {
  width: 100%;
  overflow-x: auto;
  padding: 20px 40px;
  box-sizing: border-box;
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.horizontal-list {
  display: flex;
  gap: 20px;
  padding: 0;
  margin: 0;
  list-style: none;
  scroll-behavior: smooth;
  flex-wrap: nowrap;
}

.list-item {
  flex: 0 0 auto;
  width: 125px;
  max-width: calc(100% - 40px);
  background-color: white;
  border: 2px solid #1a365d; 
  border-radius: 4px; 
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
  overflow: hidden;
}

.list-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.item-content {
  display: flex;
  flex-direction: column;
}

.item-name {
  background-color: var(--glacierWater);
  color: var(--mountainShadow);
  font-weight: 600;
  padding: 12px;
  font-size: 1.1em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
  letter-spacing: 0.5px;
}

.quantity-box {
  padding: 15px;
  background-color: var(ligh);
  border-top: 2px solid #1a365d;
}

.item-type {
  color: var(--mountainShadow);
  font-size: 1em;
  font-weight: 500;
  display: block;
  text-align: center;
}


@media (max-width: 640px) {
  .scroll-container {
    padding: 20px 30px;
  }
  
  .list-item {
    width: 180px;
  }
  
  .scroll-arrow {
    width: 32px;
    height: 32px;
  }
  
  .arrow-icon {
    font-size: 18px;
  }
}
</style>