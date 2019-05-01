<?php

namespace Silk\Recomm\Model\Resource;

use Magento\Framework\Model\ResourceModel\Db\AbstractDb;

class Group extends AbstractDb
{
    /**
     * Define main table
     */
    protected function _construct()
    {
        $this->_init('rec_product_list', 'id');
    }
}
