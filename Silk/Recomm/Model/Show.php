<?php
namespace Silk\Recomm\Model;
/**
 * Class Rule
 */
class Show implements \Magento\Framework\Option\ArrayInterface
{
    /**
     * Options getter
     *
     * @return array
     */
    public function toOptionArray()
    {
        return [
        	['value' => 'thumb', 'label' => __('Thumbnail')],
        	['value' => 'name', 'label' => __('Name')],
        	['value' => 'sku', 'label' => __('SKU')],
        	['value' => 'description', 'label' => __('Description')],
        	['value' => 'review', 'label' => __('Review')],
        	['value' => 'price', 'label' => __('Price')],
        	['value' => 'addtocart', 'label' => __('Add to cart')],
        	['value' => 'addto', 'label' => __('Wishlist - Compare')]
        ];
    }
    /**
     * Get options in "key-value" format
     *
     * @return array
     */
    public function toArray()
    {
        return [
        	['value' => 'thumb', 'label' => __('Thumbnail')],
        	['value' => 'name', 'label' => __('Name')],
        	['value' => 'sku', 'label' => __('SKU')],
        	['value' => 'description', 'label' => __('Description')],
        	['value' => 'review', 'label' => __('Review')],
        	['value' => 'price', 'label' => __('Price')],
        	['value' => 'addtocart', 'label' => __('Add to cart')],
        	['value' => 'addto', 'label' => __('Wishlist - Compare')]
        ];
    }
}
