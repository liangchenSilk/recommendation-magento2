<?php

namespace Silk\Recomm\Block;

class Result extends \Magento\Framework\View\Element\Template
{
    protected $recentlyViewed;

    public function __construct(
        \Magento\Framework\View\Element\Template\Context $context,
        \Magento\Reports\Block\Product\Viewed $recentlyViewed,
        array $data = []
    ) {
        $this->recentlyViewed = $recentlyViewed;
        parent::__construct( $context, $data);
    }

    public function getRecentlyViewed(){
	echo "test\n";
        return $this->recentlyViewed->getItemsCollection();
        //return $this->recentlyViewed->getItemsCollection()->getData();
    }
}
