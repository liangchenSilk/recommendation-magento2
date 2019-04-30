<?php
namespace Silk\Recomm\Block\Product;

use Magento\Framework\App\ObjectManager;
use Magento\Framework\DataObject\IdentityInterface;
use Magento\Framework\Pricing\PriceCurrencyInterface;
use Magento\Framework\Serialize\Serializer\Json;
use Magento\Widget\Block\BlockInterface;

use Silk\Recomm\Model\GroupFactory;
 
class ProductsList extends \Magento\CatalogWidget\Block\Product\ProductsList
{

    protected $catalogProductVisibility;
    protected $productStatus;

    protected $urlHelper;
    protected $imageHelperFactory;
    
    protected $groupFactory;
    protected $recentViewedProducts;
    
    public function __construct (
	\Magento\Catalog\Block\Product\Context $context,
        \Magento\Catalog\Model\ResourceModel\Product\CollectionFactory $productCollectionFactory,
        \Magento\Catalog\Model\Product\Visibility $catalogProductVisibility,
	\Magento\Catalog\Model\Product\Attribute\Source\Status $productStatus,
        \Magento\Framework\App\Http\Context $httpContext,
        \Magento\Rule\Model\Condition\Sql\Builder $sqlBuilder,
        \Magento\CatalogWidget\Model\Rule $rule,
        \Magento\Widget\Helper\Conditions $conditionsHelper,
	\Magento\Catalog\Helper\ImageFactory $imageHelperFactory,
	\Magento\Framework\Url\Helper\Data $urlHelper,
	\Codazon\ProductFilter\Block\ImageBuilderFactory $customImageBuilderFactory,
        array $data = [],
        Json $json = null,
        \Magento\Reports\Block\Product\Viewed $recentViewedProducts,
	GroupFactory $groupFactory
    ) {
        parent::__construct(
		$context,
		$productCollectionFactory,
		$catalogProductVisibility,
		$httpContext,
		$sqlBuilder,
		$rule,
		$conditionsHelper,
		$data,
		$json
	);
	$this->catalogProductVisibility = $catalogProductVisibility;
	$this->productStatus = $productStatus;
	$this->urlHelper = $urlHelper;
	$this->imageHelperFactory = $imageHelperFactory;
	$this->customImageBuilderFactory = $customImageBuilderFactory;

        $this->recentViewedProducts = $recentViewedProducts;
	$this->groupFactory = $groupFactory;
    }    

    public function createCollection()
    {	
/**
	if(true) {
		$recentViewedCollection = $this->recentViewedProducts->getItemsCollection();
		return $recentViewedCollection;
	}
**/
	$groupModel = $this->groupFactory->create();

	$recommSkus = [];
	$recommendCollection = $this->productCollectionFactory->create()
				 ->addAttributeToSelect('*')
				 ->addAttributeToFilter('sku', array('in' => []));

	/**
	   get collection from current viewing product
	**/
	$currentProduct = $this->getProduct();
	if($currentProduct) {
		$currentSku = $currentProduct->getSku();
		$currentGroup = $groupModel->load($currentSku, 'product_sku')
					   ->getData('group_id');
		$currentGroupSkus = $groupModel->getCollection()
						->addFieldToFilter('group_id', array('eq' => $currentGroup))
						->addFieldToSelect('product_sku')
						->getData('product_sku');
		shuffle($currentGroupSkus);
		for($i = 0; $i < min(5, count($currentGroupSkus)); $i++) {
			$recommSkus[] = $currentGroupSkus[$i]['product_sku'];
		}
	}
	/**
	  get collection from recent viewed products
	**/
	$preIndex = 1;
	$recentViewedCollection = $this->recentViewedProducts->getItemsCollection();
	foreach ($recentViewedCollection as $viewedProduct) {
		$sku = $viewedProduct->getSku();
		//echo "Pre ".$preIndex.": ".$sku."|\n";
		$preIndex += 1;
		$group_id = $groupModel->load($sku, 'product_sku')->getData('group_id');
		//echo $group_id;
		$skus = $groupModel->getCollection()
			   ->addFieldToFilter('group_id', array('eq' => $group_id))
			   ->addFieldToSelect('product_sku')
			   ->getData('product_sku');
		/**
		$randIndex = array_rand($skus, min(3, count($skus)));
		foreach($randIndex as $index) {
			$recommSkus[] = $skus[$index]['product_sku'];
		}
		**/
		shuffle($skus);
		for($i = 0; $i < min(3, count($skus)); $i++) {
			$recommSkus[] = $skus[$i]['product_sku'];
		}
	}
	
	$recommSkus = array_unique($recommSkus);
	//print_r($recommSkus);
	//echo $skus->load()->getSelect();
	foreach($recommSkus as $sku) {
		$singleCollection = $this->productCollectionFactory->create()
				 ->addAttributeToSelect('*')
				 ->addAttributeToFilter('sku', array('eq' => $sku))
				 ->addAttributeToFilter('status', ['in' => $this->productStatus->getVisibleStatusIds()]);
		$singleCollection->setVisibility($this->catalogProductVisibility->getVisibleInSiteIds());
		foreach($singleCollection as $_item) {
        		$recommendCollection->addItem($_item);
		}
	}
	/**
		filter product collection on visibility and status
	**/
	return $recommendCollection;
	//$recommCollection->addPriceData();	
	//return $recentViewedCollection;
    }
    
    public function getCacheKeyInfo()
    {
        $conditions = $this->getData('conditions')
            ? $this->getData('conditions')
            : $this->getData('conditions_encoded');
		$conditions = json_encode($this->getData());
        return [
            'PRODUCT_FILTER_WIDGET',
            $this->_storeManager->getStore()->getId(),
            $this->_storeManager->getStore()->getCurrentCurrency()->getCode(),
            $this->_design->getDesignTheme()->getId(),
            $this->httpContext->getValue(\Magento\Customer\Model\Context::CONTEXT_GROUP),
            intval($this->getRequest()->getParam(self::PAGE_VAR_NAME, 1)),
            $this->getProductsPerPage(),
            $conditions
        ];
    }

    public function getAddToCartUrl($product, $additional = [])
    {
        return $this->_cartHelper->getAddUrl($product, $additional);
    }

    public function getAddToCartPostParams(\Magento\Catalog\Model\Product $product, $additional = [])
    {
        $objectManager = \Magento\Framework\App\ObjectManager::getInstance();
        $listBlock = $objectManager->get('\Magento\Catalog\Block\Product\ListProduct');
        $url =  $listBlock->getAddToCartUrl($product);
        //$url = $this->getAddToCartUrl($product,$additional);
        return [
            'action' => $url,
            'data' => [
                'product' => $product->getEntityId(),
                \Magento\Framework\App\ActionInterface::PARAM_NAME_URL_ENCODED =>
                    $this->urlHelper->getEncodedUrl($url),
            ]
        ];
    }

    public function getIdentities()
    {
        return [\Magento\Catalog\Model\Product::CACHE_TAG];
    }

    public function getTemplate()
    {
        $template = $this->getData('filter_template');
        if($template == 'custom')
        {
            return $this->getData('custom_template');
        }
        else
        {
            return $template;
        }
    }

    public function isShow($item)
    {
    	$show = explode(",",$this->getData('show'));    	    	
    	if (in_array($item,$show) !== false) {
			return true;
		}else{
			return false;
		}
    }

    public function getImage($product, $imageId, $attributes = [])
    {
        $width = $this->getData('thumb_width');
        $height = $this->getData('thumb_height');
        $attributes = array('resize_width'=>$width,'resize_height'=>$height);
        $imageBuilder = $this->customImageBuilderFactory->create();
        return $imageBuilder->setProduct($product)
            ->setImageId($imageId)
            ->setAttributes($attributes)
            ->create();
        return $html;
    }

    public function getBlockId()
    {
    	return uniqid("rec_block_");
    }

    protected function _toHtml(){
        $isAjax = $this->getData('is_ajax');
        $isAjax = true;
        if($isAjax){
            return parent::_toHtml();
	}else{
	    $data = [
                'is_ajax'           =>  1,
                'title'             =>  $this->getData('title'),
                'display_type'      =>  $this->getData('display_type'),
                'products_count'    =>  $this->getData('products_count'),
                'order_by'          =>  $this->getData('order_by'),
                'show'              =>  $this->getData('show'),
                'thumb_width'       =>  $this->getData('thumb_width'),
                'thumb_height'      =>  $this->getData('thumb_height'),
                'filter_template'   =>  $this->getData('filter_template'),
                'custom_template'   =>  $this->getData('custom_template'),
                'show_slider'       =>  $this->getData('show_slider'),
                'slider_item'       =>  $this->getData('slider_item'),
                'conditions_encoded'        =>  $this->getData('conditions_encoded')
            ];
            $block = $this->getLayout()->createBlock('\Magento\Framework\View\Element\Template');
            $block->setTemplate('Silk_Recomm::ajax/first_load.phtml');
            $block->setData('json_data',json_encode($data));
            return $block->toHtml();
	}
     }

}
