<?php

namespace Silk\Recomm\Model;

use Magento\Framework\Model\AbstractModel;

class Group extends AbstractModel
{
    /**
     * Define resource model
     */
    protected function _construct()
    {
        $this->_init('Silk\Recomm\Model\Resource\Group');
    }
}
